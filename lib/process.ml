open Core

module Process (F : Wrapper.File.Wrapper_t.File_wrapper_t) : sig
  val postgres_module_of_file :
    fs:F.state ->
    file_path:Fpath.t ->
    base_path:Fpath.t ->
    (Postgres.Module.postgres_module, string) Either.t

  val postgres_modules_of_folder :
    fs:F.state ->
    base_path:Fpath.t ->
    ((Postgres.Module.postgres_module, string) Either.t list, string) Either.t
end = struct
  module FExt = Wrapper.File.Extensions.Make (F)

  let module_name_of_file_path ~file_path ~base_path =
    match Fpath.relativize ~root:base_path file_path with
    | None -> None
    | Some relative_path ->
        let parent, base = Fpath.split_base relative_path in
        let base_without_extension = Fpath.rem_ext base in
        let base_string = Fpath.to_string base_without_extension in
        let renamed_base =
          match String.lsplit2 base_string ~on:'_' with
          | None -> base_string
          | Some (prefix, suffix) -> (
              match Int.of_string_opt prefix with
              | None -> base_string
              | Some _ -> suffix)
        in
        Some (Fpath.segs (Fpath.add_seg parent renamed_base))

  let postgres_module_of_file ~fs ~file_path ~base_path =
    match module_name_of_file_path ~file_path ~base_path with
    | None -> Second "Could not get module name"
    | Some module_name -> (
        let read_result = F.read_file fs file_path in
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

  let postgres_modules_of_folder ~fs ~base_path =
    FExt.files_of_directory_with_extension ~fs ~recurse:true ~extension:".sql"
      base_path
    |> function
    | Second msg -> Second msg
    | First files ->
        List.sort ~compare:Fpath.compare files
        |> List.map ~f:(fun file_path ->
               postgres_module_of_file ~fs ~base_path ~file_path)
        |> fun x -> First x
end
