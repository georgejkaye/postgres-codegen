type postgres_module = {
  module_name : string list;
  statements : Statement.statement list;
}
[@@deriving show]
