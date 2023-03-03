import copy
import io
import json
import os
import re

import yaml
from django.core.serializers.json import DjangoJSONEncoder
from jsonschema import FormatChecker
from jsonschema.validators import Draft7Validator
from jsonschema.validators import extend

import jsonref

re_uuid = re.compile("[0-F]{8}-([0-F]{4}-){3}[0-F]{12}", re.I)
checker = FormatChecker()

API_YAML_PATH = os.environ.get('API_YAML_PATH', '../../../api/api.yaml')


def load_schema(filename):
    with open(filename) as fobj:
        inst_with_ref = yaml.load(fobj, Loader=yaml.SafeLoader)
    inst = jsonref.loads(
        json.dumps(
            inst_with_ref,
            indent=1,
            cls=DjangoJSONEncoder,
        )
    )

    def recursive_null_setter(root):
        if isinstance(root, list):
            root = [recursive_null_setter(item) for item in root]
        elif isinstance(root, dict):
            root = copy.deepcopy(root)
            if 'nullable' in root:
                if 'type' in root:
                    root['type'] = [root['type'], 'null']
                else:
                    root['type'] = 'null'
            for (k, v) in root.items():
                root[k] = recursive_null_setter(v)
        return root
    return recursive_null_setter(inst)


_SCHEMA_FILENAME = os.path.join(os.path.dirname(__file__), API_YAML_PATH)
_SCHEMA = load_schema(_SCHEMA_FILENAME)


def is_io(checker, instance):
    return (
        Draft7Validator.TYPE_CHECKER.is_type(instance, "string") or
        isinstance(instance, io.BytesIO)
    )


@checker.checks("binary", raises=ValueError)
def check(instance):
    return isinstance(instance, io.BytesIO)


CustomValidator = extend(
    Draft7Validator,
    type_checker=Draft7Validator.TYPE_CHECKER.redefine("string", is_io)
)


def validate_response(uri, method, code, body, content_type='application/vnd.api+json'):
    uri = re_uuid.sub('{itemId}', uri)
    uri = '/' + '/'.join(uri.split('/')[3:])
    uri = uri.replace('$', '').replace('^', '')

    endpoint = _SCHEMA['paths'][uri][method]['responses']
    code = str(code)
    if code in endpoint:
        schema = endpoint[code]['content'][content_type]['schema']['properties']['data']
    else:
        schema = endpoint['default']['content'][content_type]['schema']['properties']
    return CustomValidator(schema).validate(body)


def validate_request(uri, method, body: dict = None, content_type='application/json'):
    uri = re_uuid.sub('{itemId}', uri)
    uri = '/' + '/'.join(uri.split('/')[3:])
    uri = uri.replace('$', '').replace('^', '')

    # For methods without body(GET, DELETE). Validate to exists endpoint in schema.
    method_schema = _SCHEMA['paths'][uri][method]
    if method in ['get', 'delete'] and body is None and 'requestBody' not in method_schema:
        return True

    schema = method_schema['requestBody']['content'][content_type]['schema']
    if content_type == 'multipart/form-data' and 'data' in body:
        try:
            body = copy.deepcopy(body)
        except TypeError:
            body = body.copy()

        try:
            body['data'] = json.loads(body.get('data'))
        except Exception:
            pass

    return CustomValidator(schema, format_checker=checker).validate(body)
