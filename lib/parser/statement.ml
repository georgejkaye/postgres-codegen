open Angstrom
open Postgres.Statement

let ws =
  skip_while (function '\x20' | '\x0a' | '\x0d' | '\x09' -> true | _ -> false)

let lchar c = ws *> char c
let lstring s = ws *> string_ci s
let lb = lchar '('
let rb = lchar ')'
let comma = lchar ','
let or_replace = lstring "OR" *> ws *> lstring "REPLACE"
let create_keyword = lstring "CREATE"

let identifier =
  take_till (function ' ' | ',' | '(' | ')' | ';' -> true | _ -> false)

let type_identifier =
  ws *> identifier <* ws >>= fun id ->
  return (Postgres.Types.postgres_type_of_string id)

let returns = ws *> lstring "RETURNS" *> type_identifier

let param_and_type =
  both (ws *> identifier <* ws) (ws *> type_identifier <* ws)
  >>= fun (id, type_id) ->
  return { parameter_name = id; parameter_type = type_id }

let bracketed_params =
  ws *> lb *> ws *> sep_by comma param_and_type <* ws <* rb <* ws

let _function =
  both
    (lstring "FUNCTION" *> ws *> identifier <* ws)
    (both bracketed_params returns)
  >>= fun (function_name, (parameters, return_type)) ->
  return (Create (Function (function_name, parameters, return_type)))

let _type = lstring "TYPE" *> return (Create (Type ("hello", [])))
let _domain = lstring "DOMAIN" *> return (Create (Domain ("hello", "Hello")))

let create_or_replace =
  lstring "CREATE" *> ws *> many or_replace *> ws *> peek_char_fail >>= function
  | 'F' -> _function
  | 'T' -> _type
  | 'D' -> _domain
  | _ -> fail "Invalid create"

let drop = lstring "DROP" *> return (Drop (Function, "Hello"))
let language = lstring "LANGUAGE"
let as_ = lstring "AS"
let dollars = lstring "$$"
let sc = lchar ';'

let statement =
  ws *> peek_char_fail >>= function
  | 'C' -> create_or_replace
  | 'D' -> drop
  | _ -> fail "Not supported"
