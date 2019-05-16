from inspect import isclass
from flask_restplus import Api, Swagger, Model, fields
from flask_restplus.swagger import ref, PY_TYPES
from six import string_types
from flask_restplus import apidoc


class MyAPI(Api):
    def __schema__(self):
        '''
        The Swagger specifications/schema for this API

        :returns dict: the schema as a serializable dict
        '''
        if not self._schema:
            self._schema = mySwagger(self).as_dict()
        return self._schema

    def render_doc(self):
        '''Override this method to customize the documentation page'''
        self.abort(404)

    def my_render_doc(self):
        '''Override this method to customize the documentation page'''
        return apidoc.ui_for(self)


class mySwagger(Swagger):
    def serialize_schema(self, model):
        if isinstance(model, (list, tuple)):
            model = model[0]
            return {
                'type': 'array',
                'items': self.serialize_schema(model),
            }

        elif isinstance(model, Model):
            self.register_model(model)
            return ref(model)

        elif isinstance(model, dict):
            out = {}

            [out.update({k: self.serialize_schema(model[k])}) for k in model]

            return {'properties': out}

        elif isinstance(model, string_types):
            self.register_model(model)
            return ref(model)

        elif isclass(model) and issubclass(model, fields.Raw):
            return self.serialize_schema(model())

        elif isinstance(model, fields.Raw):
            return model.__schema__

        elif isinstance(model, (type, type(None))) and model in PY_TYPES:
            return {'type': PY_TYPES[model]}

        raise ValueError('Model {0} not registered'.format(model))
