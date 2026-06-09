type drop_parameters = {
  object_type : Object_type.postgres_object_type;
  object_name : string;
  cascade : bool;
}
[@@deriving show]

type statement = Create of Object.postgres_object | Drop of drop_parameters
[@@deriving show]
