open Core

type create_parameters = {
  object_data : Object.postgres_object;
  or_replace : bool;
}
[@@deriving show, compare, make]

type drop_parameters = {
  object_type : Object_type.postgres_object_type;
  object_name : string;
  if_exists : bool;
  cascade : bool;
}
[@@deriving show, compare]

type statement = Create of create_parameters | Drop of drop_parameters
[@@deriving show, compare, variants]

let make_create_composite ~or_replace composite_name composite_fields =
  create
    (make_create_parameters
       ~object_data:
         (Object.composite
            (Composite.make_postgres_composite ~composite_name ~composite_fields
               ()))
       ~or_replace)
