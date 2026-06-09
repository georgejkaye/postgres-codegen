open Core

module Base_file_wrapper : Wrapper_t.File_wrapper_t = struct
  let read_file path =
    match Util.File.file_exists path with
    | `No -> Second [%string "File %{Fpath.to_string path} does not exist"]
    | `Unknown ->
        Second
          [%string "Cannot determine if file %{Fpath.to_string path} exists"]
    | `Yes ->
        First
          (Util.File.with_in_file ~binary:false
             ~f:(fun file -> In_channel.input_all file)
             path)

  let write_file path s =
    Util.File.with_out_file path ~binary:false ~f:(fun file ->
        Out_channel.output_string file s)
end
