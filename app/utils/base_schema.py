from pydantic import BaseModel, ConfigDict

def snake_to_camel(name: str) -> str:
    """
    Fungsi Convert snake_case(schema) to camelCase(input)
    Contoh:
        diameter_pole  -> diameterPole
        area_front_do  -> areaFrontDo
        cf_do          -> cfDo

    digunakan untuk generate alias based on deklarasi schema
    """
    components = name.split("_")
    # mengubah komponent sebelah kanan setelah di split menjadi capital
    return components[0] + "".join(word.capitalize() for word in components[1:])


class CamelBaseModel(BaseModel):
    """
    Pemakaian cukup panggil sebagai parent:
        class PoleInput(CamelBaseModel):
            diameter_pole: float       
            height_pole: float         
            material_pole: str         

    model_config breakdown:
        alias_generator     — auto-generates camelCase alias untuk setiap fields
        populate_by_name    — juga menerima snake_case input (bisa untuk testing / untuk forward snake_case in response)
        from_attributes     — menerima building the model from ORM objects (untuk Database)
    """

    model_config = ConfigDict(
        alias_generator=snake_to_camel,
        populate_by_name=True,  
        from_attributes=True,
    )
