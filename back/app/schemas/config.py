from pydantic import ConfigDict
from pydantic.alias_generators import to_camel

config = ConfigDict(
    populate_by_name=True,
    alias_generator=to_camel,
    from_attributes=True,
    arbitrary_types_allowed=True,
)
