open Core

module Base_file_wrapper : Wrapper.File_wrapper = struct
  let read_file =
    In_channel.with_file ~binary:false ~f:(fun file ->
        In_channel.input_all file)

  let write_file path s =
    Out_channel.with_file path ~f:(fun file -> Out_channel.output_string file s)
end
