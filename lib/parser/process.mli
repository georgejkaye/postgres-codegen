open Core

val get_postgres_objects_for_file_contents :
  string -> (Postgres.Object.postgres_object, string) Either.t list
