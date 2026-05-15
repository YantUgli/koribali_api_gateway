import re


def camel_to_snake(name: str) -> str:
    """
    Mengubah camelCase to snake_case

    Contoh:
        diameterPole  -> diameter_pole
        areaFrontDo   -> area_front_do
        cfDo          -> cf_do
        nameDo        -> name_do
    """
    # memecah setiap ada Capital Menjadi underscore
    s = re.sub(r"([A-Z])", r"_\1", name)

    # mengubah huruf setelah underscore menjadi lowecase
    return s.lstrip("_").lower()
