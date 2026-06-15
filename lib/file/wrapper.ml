open Core

module System_file_wrapper : Wrapper_t.File_wrapper_t = struct
  type state = unit

  let init_state = ()
  let is_dir () path = Sys_unix.is_directory (Fpath.to_string path)
  let file_exists () path = Sys_unix.file_exists (Fpath.to_string path)

  let with_out_file path ?(binary = false) =
    Core.Out_channel.with_file ~binary (Fpath.to_string path)

  let with_in_file path ?(binary = false) =
    Core.In_channel.with_file ~binary (Fpath.to_string path)

  let read_file () path =
    match file_exists () path with
    | `No -> Second [%string "File %{Fpath.to_string path} does not exist"]
    | `Unknown ->
        Second
          [%string "Cannot determine if file %{Fpath.to_string path} exists"]
    | `Yes ->
        First
          (with_in_file ~binary:false
             ~f:(fun file -> In_channel.input_all file)
             path)

  let write_file _ path s =
    with_out_file path ~binary:false ~f:(fun file ->
        Out_channel.output_string file s)

  let rec files_of_directory () ?(filter = fun _ -> true) ?(recurse = false)
      dir_path =
    let files = Sys_unix.ls_dir (Fpath.to_string dir_path) in
    let full_files =
      List.fold
        ~f:(fun acc file_name ->
          let open Fpath in
          let full_path = dir_path / file_name in
          let acc = if filter full_path then full_path :: acc else acc in
          if not recurse then acc
          else
            match is_dir () full_path with
            | `Yes ->
                let subdir_files =
                  files_of_directory () full_path ~recurse:true ~filter
                in
                subdir_files @ acc
            | _ -> acc)
        ~init:[] files
    in
    List.rev full_files
end
