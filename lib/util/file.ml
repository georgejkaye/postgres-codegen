open Core

let file_exists path = Sys_unix.file_exists (Fpath.to_string path)

let with_out_file path ?(binary = false) =
  Core.Out_channel.with_file ~binary (Fpath.to_string path)

let with_in_file path ?(binary = false) =
  Core.In_channel.with_file ~binary (Fpath.to_string path)

let of_string path_string =
  match Fpath.of_string path_string with
  | Error msg -> Second msg
  | Ok a -> First a
