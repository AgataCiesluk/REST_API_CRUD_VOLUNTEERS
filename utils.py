def sqlalchemy_model_to_dict(model):
    model_dict = model.__dict__
    model_dict.pop('_sa_instance_state')
    return model_dict


def models_list_to_dict(models_list):
    return [sqlalchemy_model_to_dict(model) for model in models_list]
