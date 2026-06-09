open Postgres_codegen
open Core

let params =
  let open Command.Param in
  both (anon ("filename" %: string)) (anon ("base" %: string))

module Parser = Parser.Process.Process (File.Wrapper.Base_file_wrapper)

let get_postgres_objects = Parser.postgres_module_of_file
let print_message = Util.Show.show_line (fun x -> x)

let print_error_or_result = function
  | Second msg -> print_message msg
  | First objects ->
      let open Postgres.Module in
      List.iter
        ~f:(Util.Show.show_line Postgres.Statement.show_statement)
        objects.statements

let command =
  Command.basic ~summary:"Generate code for interacting with postgres objects"
    ~readme:(fun () -> "Todo")
    (Command.Param.map params ~f:(fun (file_path, base_path) () ->
         let file_path = Util.File.of_string file_path in
         let base_path = Util.File.of_string base_path in
         match (file_path, base_path) with
         | First file_path, First base_path ->
             get_postgres_objects ~file_path ~base_path |> print_error_or_result
         | Second _, _ -> print_message "Could not parse file path"
         | _, Second _ -> failwith "Could not parse base path"))

let () = Command_unix.run ~version:"1.0" ~build_info:"RWO" command
