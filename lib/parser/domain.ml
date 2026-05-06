open Core
open Postgres.Domain

module Postgres_domain_parser :
  Object.Postgres_object_parser with type t = Postgres.Domain.postgres_domain =
struct
  type t = Postgres.Domain.postgres_domain

  let get_statement_regex = "CREATE DOMAIN (.*) AS ([A-z_]*) (?:.*)"

  let postgres_object_of_match m =
    let domain_name = Re.Group.get m 1 in
    let underlying_type =
      Re.Group.get m 2 |> Postgres.Types.postgres_type_of_string
    in
    First { domain_name; underlying_type }
end

module Postgres_domain_parser_processor =
  Processor.Parser_processor (Postgres_domain_parser)
