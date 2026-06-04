type postgres_domain = {
  domain_name : string;
  underlying_type : Types.postgres_type;
}
[@@deriving show]
