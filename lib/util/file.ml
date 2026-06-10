open Core

let is_dir path = Sys_unix.is_directory (Fpath.to_string path)
let file_exists path = Sys_unix.file_exists (Fpath.to_string path)

let with_out_file path ?(binary = false) =
  Core.Out_channel.with_file ~binary (Fpath.to_string path)

let with_in_file path ?(binary = false) =
  Core.In_channel.with_file ~binary (Fpath.to_string path)

let of_string path_string =
  match Fpath.of_string path_string with
  | Error msg -> Second msg
  | Ok a -> First a

let rec get_files_in_directory ?(filter = fun _ -> true) ?(recurse = false)
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
          match is_dir full_path with
          | `Yes ->
              let subdir_files =
                get_files_in_directory full_path ~recurse:true ~filter
              in
              subdir_files @ acc
          | _ -> acc)
      ~init:[] files
  in
  List.rev full_files

let get_files_in_directory_with_extension ?(recurse = false) ~extension =
  get_files_in_directory
    ~filter:(fun full_path -> equal_string (Fpath.get_ext full_path) extension)
    ~recurse
