open Core

type create_parameters = {
  object_data : Object.postgres_object;
  or_replace : bool;
}
[@@deriving show, compare]

type drop_parameters = {
  object_type : Object_type.postgres_object_type;
  object_name : string;
  if_exists : bool;
  cascade : bool;
}
[@@deriving show, compare]

type statement = Create of create_parameters | Drop of drop_parameters
[@@deriving show, compare]
