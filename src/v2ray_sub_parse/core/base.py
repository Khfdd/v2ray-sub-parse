import pydantic
import pydantic.alias_generators


class Base(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(
        strict=True,
        frozen=True,
        use_enum_values=True,
        populate_by_name=True,
        alias_generator=pydantic.alias_generators.to_camel
    )
