open Core
open Postgres.Domain

module Postgres_domain_parser : Object.Postgres_object_parser_t = struct
  type t = Postgres.Domain.postgres_domain

  let get_statement_regex = "CREATE DOMAIN (.*) AS ([A-z_]*) (?:.*)"

  let of_match m =
    let domain_name = Re.Group.get m 1 in
    let underlying_type =
      Re.Group.get m 2 |> Postgres.Types.postgres_type_of_string
    in
    First { domain_name; underlying_type }

  let to_object d = Postgres.Object.Domain d
end

module Postgres_domain = struct
  include Postgres.Domain.Postgres_domain
  include Make.Make_parser (Postgres_domain_parser)
end
