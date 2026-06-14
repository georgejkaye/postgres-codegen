open Core

module Process (F : File.Wrapper_t.File_wrapper_t) : sig
  val postgres_module_of_file :
    file_path:Fpath.t ->
    base_path:Fpath.t ->
    (Postgres.Module.postgres_module, string) Either.t

  val postgres_modules_of_folder :
    base_path:Fpath.t -> (Postgres.Module.postgres_module, string) Either.t list
end = struct
  let module_name_of_file_path ~file_path ~base_path =
    match Fpath.relativize ~root:base_path file_path with
    | None -> None
    | Some relative_path -> (
        let segments = Fpath.segs relative_path in
        match List.rev segments with
        | [] -> None
        | x :: xs -> (
            match String.lsplit2 ~on:'.' x with
            | Some (name, _) -> Some (List.rev (name :: xs))
            | None -> Some segments))

  let postgres_module_of_file ~file_path ~base_path =
    match module_name_of_file_path ~file_path ~base_path with
    | None -> Second "Could not get module name"
    | Some module_name -> (
        let read_result = F.read_file file_path in
        match read_result with
        | Second error ->
            Second [%string "ERROR: %{Fpath.to_string file_path}: %{error}"]
        | First contents -> (
            let open Postgres.Module in
            match Parser.Process.parse_statements contents with
            | Ok statements ->
                let statements = Util.List.filter_somes statements in
                First { module_name; statements }
            | Error msg ->
                Second [%string "ERROR: %{Fpath.to_string file_path}: %{msg}"]))

  let postgres_modules_of_folder ~base_path =
    Util.File.get_files_in_directory_with_extension ~recurse:true
      ~extension:".sql" base_path
    |> List.sort ~compare:Util.File.compare
    |> List.map ~f:(fun file_path ->
           postgres_module_of_file ~base_path ~file_path)
end
