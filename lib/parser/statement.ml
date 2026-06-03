open Angstrom
open Postgres.Statement
open Util
open Combinators

let function_header_keywords = [ "LANGUAGE"; "RETURNS"; "AS" ]
let lb = char_ws '('
let rb = char_ws ')'
let comma = char_ws ','
let dollars = string_ci_ws "$$"
let sc = char_ws ';'

let or_replace =
  many (string_ci_ws "OR" *> string_ci_ws "REPLACE" *> return ())
  >>= (fun rs ->
        match List.length rs with
        | 0 | 1 -> return ()
        | _ -> fail "Too many OR REPLACE")
  <?> "or_replace"

let variable_name =
  take_while1 (function
    | ' ' | ',' | '(' | ')' | ';' | '\n' | '\r' -> false
    | _ -> true)
  <* ws
  <?> "variable_name"

let type_name =
  take_while1 (function
    | '(' | ')' | ',' | ';' | '\n' | '\r' -> false
    | _ -> true)
  >>= fun t ->
  return (Postgres.Types.postgres_type_of_string (String.strip t))
  <* ws
  <?> "type_name"

let param_and_type =
  variable_name ^^ type_name >>= fun (parameter_name, parameter_type) ->
  return { parameter_name; parameter_type } <?> "param_and_type"

let bracketed_params =
  lb *> sep_by comma param_and_type <* ws <* rb <?> "bracketed_params"

let language =
  variable_name
  >>= (fun id ->
        match Postgres.Language.of_string id with
        | Some l -> return l
        | None -> fail ("Invalid language " ^ id))
  <?> "language"

let keyword kw = string_ci_ws kw <?> "expected keyword " ^ kw
let as_keyword = keyword "AS"
let function_keyword = keyword "FUNCTION"
let returns_keyword = keyword "RETURNS"
let language_keyword = keyword "LANGUAGE"
let double_dollars = string_ci_ws "$$" <?> "expected $$"

let dollar_surrounded_body =
  double_dollars *> take_till_string1 "$$"
  <* double_dollars
  <?> "dollar_surrounded_body"

let statement_body = take_till_char ';' <?> "statement_body"

let function_body =
  peek_char_fail
  >>= (function '$' -> dollar_surrounded_body | _ -> statement_body)
  <?> "function_body"

let function_return_type =
  take_till_distinct_strings1 function_header_keywords
  >>= (fun t ->
        return (Postgres.Types.postgres_type_of_string (String.strip t)) <* ws)
  <?> "function_return_type"

let function_statement =
  (let+ _ = function_keyword
   and+ function_name = variable_name
   and+ parameters = bracketed_params
   and+ _ = returns_keyword
   and+ return_type = function_return_type
   and+ _ = language_keyword
   and+ lang = language
   and+ _ = as_keyword
   and+ body = function_body in
   Create (Function (function_name, parameters, return_type, lang, body)))
  <?> "function_statement"

let type_statement = string_ci_ws "TYPE" *> return (Create (Type ("hello", [])))

let domain_statement =
  string_ci_ws "DOMAIN" *> return (Create (Domain ("hello", "Hello")))

let create_or_replace =
  string_ci_ws "CREATE" *> or_replace <?> "create_or_replace"

let create_body =
  peek_char_fail
  >>= (function
        | 'F' -> function_statement
        | 'T' -> type_statement
        | 'D' -> domain_statement
        | _ -> fail "Invalid create")
  <?> "create_body"

let drop = string_ci_ws "DROP" *> return (Drop (Function, "Hello"))

let statement =
  ws *> peek_char_fail
  >>= (function
        | 'C' -> create_or_replace *> create_body
        | 'D' -> drop
        | _ -> fail "Not supported")
  <* sc
  <?> "statement"

let statements = many statement <?> "statements"
