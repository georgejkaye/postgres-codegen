open Postgres_codegen
open Core
open Util

let param =
  let open Command.Param in
  anon ("filename" %: string)

let read_file = File.Wrapper.Base_file_wrapper.read_file
let get_postgres_objects = Parser.Process.get_postgres_objects_for_file_contents

let print_objects =
  List.iter ~f:(Show.show_line Postgres.Object.show_postgres_object)

let print_message = Show.show_line (fun x -> x)

let print_error_or_result = function
  | Second msg -> print_message msg
  | First objects -> print_objects objects

let get_objects = function
  | Second msg -> Second msg
  | First contents -> First (get_postgres_objects contents)

let command =
  Command.basic ~summary:"Generate code for interacting with postgres objects"
    ~readme:(fun () -> "Todo")
    (Command.Param.map param ~f:(fun filename () ->
         filename |> read_file |> get_objects |> print_error_or_result))

let () = Command_unix.run ~version:"1.0" ~build_info:"RWO" command
