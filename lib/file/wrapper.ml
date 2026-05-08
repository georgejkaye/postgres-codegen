open Core

module Base_file_wrapper : Wrapper_t.File_wrapper_t = struct
  let read_file path =
    match Sys_unix.file_exists path with
    | `No -> Second [%string "File %{path} does not exist"]
    | `Unknown -> Second [%string "Cannot determine if file %{path} exists"]
    | `Yes ->
        First
          (In_channel.with_file ~binary:false
             ~f:(fun file -> In_channel.input_all file)
             path)

  let write_file path s =
    Out_channel.with_file path ~f:(fun file -> Out_channel.output_string file s)
end
