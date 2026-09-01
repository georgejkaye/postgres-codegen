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
[@@deriving show, compare, make]

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

let make_create_function ~or_replace function_name function_return
    function_parameters function_language function_body =
  create
    (make_create_parameters
       ~object_data:
         (Object.function_
            (Function.make_postgres_function ~function_name ~function_return
               ~function_language ~function_parameters ~function_body ()))
       ~or_replace)

let make_drop object_type ~if_exists object_name ~cascade =
  drop (make_drop_parameters ~object_type ~object_name ~if_exists ~cascade)
