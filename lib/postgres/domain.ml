open Core

type postgres_domain_constraint = NotNull | Check of string
[@@deriving show, compare]

type postgres_domain = {
  domain_name : string;
  underlying_type : Types.postgres_type;
  domain_constraint : postgres_domain_constraint;
}
[@@deriving show, compare]
