open Postgres_codegen
open Core

let params =
  let open Command.Param in
  anon ("base" %: string)

module Parser = Process.Process (File.Wrapper.Base_file_wrapper)

let get_postgres_objects = Parser.postgres_modules_of_folder
let print_message = Util.Show.show_line (fun x -> x)

let print_error_or_result = function
  | Second msg -> print_message msg
  | First objects ->
      let open Postgres.Module in
      Util.Show.show_line
        (fun x -> x)
        (String.concat ~sep:"." objects.module_name);
      print_endline "\n";
      List.iter
        ~f:(fun s ->
          Util.Show.show_line Postgres.Statement.show_statement s;
          print_endline "")
        objects.statements;
      print_endline "\n"

let command =
  Command.basic ~summary:"Generate code for interacting with postgres objects"
    ~readme:(fun () -> "Todo")
    (Command.Param.map params ~f:(fun base_path () ->
         let base_path = Util.File.of_string base_path in
         match base_path with
         | First base_path ->
             get_postgres_objects ~base_path
             |> List.iter ~f:print_error_or_result
         | Second _ -> failwith "Could not parse base path"))

let () = Command_unix.run ~version:"1.0" ~build_info:"RWO" command
