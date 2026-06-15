open Core

module File (F : Lib.File.Wrapper_t.File_wrapper_t) = struct
  let files_of_directory_with_extension ~fs ?(recurse = false) ~extension =
    F.files_of_directory fs
      ~filter:(fun full_path ->
        equal_string (Fpath.get_ext full_path) extension)
      ~recurse
end

let of_string path_string =
  match Fpath.of_string path_string with
  | Error (`Msg msg) -> Second msg
  | Ok a -> First a
