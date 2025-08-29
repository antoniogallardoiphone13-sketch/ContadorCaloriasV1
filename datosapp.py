class ContadorCalorias:
    total_calorias_consumidas = 0
    total_calorias_gastadas = 0 

    @classmethod
    def agregar_calorias_consumidas(cls, cantidad):
        cls.total_calorias_consumidas += cantidad



    @classmethod
    def agregar_calorias_gastadas(cls, cantidad):
        cls.total_calorias_gastadas += cantidad

    @classmethod
    def obtener_total_calorias_consumidas(cls):
        return cls.total_calorias_consumidas
    
    
    @classmethod
    def obtener_total_calorias_gastadas(cls):
        return cls.total_calorias_gastadas

    def obtener_total_calorias(self):
        return self.total_calorias_consumidas - self.total_calorias_gastadas    
    

    @classmethod
    def reiniciar(cls):
        cls.total_calorias = 0