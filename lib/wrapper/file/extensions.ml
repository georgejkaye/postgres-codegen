open Core

module Make (F : Wrapper_t.File_wrapper_t) = struct
  let files_of_directory_with_extension ~fs ?(recurse = false) ~extension =
    F.files_of_directory fs
      ~filter:(fun full_path ->
        equal_string (Fpath.get_ext full_path) extension)
      ~recurse
end
