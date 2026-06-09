type postgres_composite = {
  composite_name : string;
  composite_fields : Parameter.parameter list;
}
[@@deriving show]
