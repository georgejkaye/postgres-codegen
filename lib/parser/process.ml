open Core

module Process (F : File.Wrapper_t.File_wrapper_t) : sig
  val postgres_module_of_file :
    file_path:Fpath.t ->
    base_path:Fpath.t ->
    (Postgres.Module.postgres_module, string) Either.t

  val parse_modules_from_folder :
    string -> (Postgres.Module.postgres_module list, string) Either.t
end = struct
  let module_name_of_file_path ~file_path ~base_path =
    match Fpath.relativize ~root:base_path file_path with
    | None -> None
    | Some relative_path -> Some (Fpath.segs relative_path)

  let parse_statements = Angstrom.parse_string Statement.statements ~consume:All

  let postgres_module_of_file ~file_path ~base_path =
    match module_name_of_file_path ~file_path ~base_path with
    | None -> Second "Could not get module name"
    | Some module_name -> (
        let read_result = F.read_file file_path in
        match read_result with
        | Second error -> Second error
        | First contents -> (
            let open Postgres.Module in
            match parse_statements contents with
            | Ok statements -> First { module_name; statements }
            | Error msg -> Second msg))

  let parse_modules_from_folder _ = failwith "todo"
end
