from editors.types.dataType import CgpDatas


class ShaderProps(CgpDatas):
    def __init__(self, **kwargs):
        self.set(**kwargs)

    def set(self,**kwargs):
        for key, value in kwargs.items():
            self.__dict__[key] = value
    def get(self, name):
        return self.__dict__[name]