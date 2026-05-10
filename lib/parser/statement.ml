open Angstrom
open Postgres.Statement
open Util
open Combinators

let lb = char_ws '('
let rb = char_ws ')'
let comma = char_ws ','

let or_replace =
  many (string_ci_ws "OR" *> string_ci_ws "REPLACE" *> return ()) >>= fun rs ->
  match List.length rs with
  | 0 | 1 -> return ()
  | _ -> fail "Too many OR REPLACE"

let variable_name =
  take_while1 (function ' ' | ',' | '(' | ')' | ';' -> false | _ -> true)
  <* ws

let type_name =
  take_while1 (function '(' | ')' | ',' | ';' -> false | _ -> true)
  >>= fun t ->
  return (Postgres.Types.postgres_type_of_string (String.strip t)) <* ws

let returns = string_ci_ws "RETURNS" *> type_name

let param_and_type =
  variable_name ^^ type_name >>= fun (parameter_name, parameter_type) ->
  return { parameter_name; parameter_type }

let bracketed_params = lb *> sep_by comma param_and_type <* ws <* rb

let language =
  string_ci_ws "LANGUAGE" *> variable_name >>= fun id ->
  match Postgres.Language.of_string id with
  | Some l -> return l
  | None -> fail "Invalid language"

let _as = string_ci_ws "AS"

let _function =
  (string_ci_ws "FUNCTION" *> variable_name)
  ^^ bracketed_params
  ^^ returns
  ^^ language
  <* _as
  >>= fun (function_name, (parameters, (return_type, lang))) ->
  return (Create (Function (function_name, parameters, return_type, lang)))

let _type = string_ci_ws "TYPE" *> return (Create (Type ("hello", [])))

let _domain =
  string_ci_ws "DOMAIN" *> return (Create (Domain ("hello", "Hello")))

let create_or_replace = string_ci_ws "CREATE" *> or_replace

let create_body =
  peek_char_fail >>= function
  | 'F' -> _function
  | 'T' -> _type
  | 'D' -> _domain
  | _ -> fail "Invalid create"

let drop = string_ci_ws "DROP" *> return (Drop (Function, "Hello"))
let dollars = string_ci_ws "$$"
let sc = char_ws ';'

let statement =
  ws *> peek_char_fail >>= function
  | 'C' -> create_or_replace *> create_body
  | 'D' -> drop
  | _ -> fail "Not supported"
