type postgres_composite_field = {
  field_name : string;
  field_type : Types.postgres_type;
}
[@@deriving show]

type postgres_composite = {
  composite_name : string;
  composite_fields : postgres_composite_field list;
}
[@@deriving show]
