open Angstrom
open Postgres.Statement
open Postgres
open Util
open Combinators

let function_header_keywords = [ "LANGUAGE"; "RETURNS"; "AS" ]
let lb = char_ws '('
let rb = char_ws ')'
let comma = char_ws ','
let double_dollars = string_ci_ws "$$" <?> "expected $$"
let sc = char_ws ';'
let keyword kw = string_ci_ws kw <?> "expected keyword " ^ kw
let as_keyword = keyword "AS"
let cascade_keyword = keyword "CASCADE"
let create_keyword = keyword "CREATE"
let domain_keyword = keyword "DOMAIN"
let drop_keyword = keyword "DROP"
let exists_keyword = keyword "EXISTS"
let function_keyword = keyword "FUNCTION"
let if_keyword = keyword "IF"
let language_keyword = keyword "LANGUAGE"
let or_keyword = keyword "OR"
let replace_keyword = keyword "REPLACE"
let returns_keyword = keyword "RETURNS"
let type_keyword = keyword "TYPE"
let view_keyword = keyword "VIEW"

let or_replace =
  many (or_keyword *> replace_keyword *> return ())
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

let parameter_type =
  take_while1 (function ')' | ',' -> false | _ -> true) >>= fun t ->
  return (Postgres.Types.postgres_type_of_string (String.strip t))
  <* ws
  <?> "type_name"

let param_and_type =
  variable_name ^^ parameter_type >>= fun (parameter_name, parameter_type) ->
  let open Parameter in
  return { parameter_name; parameter_type } <?> "param_and_type"

let bracketed_params =
  lb *> sep_by comma param_and_type <* ws <* rb <?> "bracketed_params"

let language_name =
  variable_name
  >>= (fun id ->
        match Postgres.Language.of_string id with
        | Some l -> return l
        | None -> fail ("Invalid language " ^ id))
  <?> "language"

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
  (let+ function_name = variable_name
   and+ function_parameters = bracketed_params
   and+ _ = returns_keyword
   and+ function_return = function_return_type
   and+ _ = language_keyword
   and+ function_language = language_name
   and+ _ = as_keyword
   and+ function_body = function_body in
   Create
     (Function
        {
          function_name;
          function_parameters;
          function_return;
          function_language;
          function_body;
        }))
  <?> "function_statement"

let type_statement =
  let+ composite_name = variable_name
  and+ _ = as_keyword
  and+ composite_fields = bracketed_params in
  Create (Composite { composite_name; composite_fields })

let domain_constraint =
  take_till_char ';' >>= function
  | "NOT NULL" -> return Domain.NotNull
  | x -> (
      match Util.String.drop_pattern_from_start x "CHECK" with
      | Some pattern -> return (Domain.Check pattern)
      | None -> fail "unsupported constraint")

let domain_type =
  take_till_distinct_strings [ "NOT"; "CHECK" ] >>= fun s ->
  return (Postgres.Types.postgres_type_of_string s)

let domain_statement =
  let+ domain_name = variable_name
  and+ _ = as_keyword
  and+ underlying_type = domain_type
  and+ domain_constraint = domain_constraint in
  Create (Domain { domain_name; underlying_type; domain_constraint })

let view_statement = fail "todo"

let object_type =
  peek_char_fail >>= function
  | 'F' -> function_keyword *> return Object_type.Function
  | 'T' -> type_keyword *> return Object_type.Composite
  | 'D' -> domain_keyword *> return Object_type.Domain
  | 'V' -> view_keyword *> return Object_type.View
  | _ -> fail "unsupported drop" <?> "drop"

let create =
  create_keyword *> or_replace *> object_type
  >>= (function
        | Object_type.Function -> function_statement
        | Object_type.Composite -> type_statement
        | Object_type.Domain -> domain_statement
        | Object_type.View -> view_statement)
  <?> "create"

let if_exists = at_most_one (if_keyword *> exists_keyword *> return ())

let drop =
  drop_keyword *> object_type >>= fun object_type ->
  (if_exists *> variable_name) ^^ at_most_one cascade_keyword
  >>= fun (object_name, (i, _)) ->
  return (Drop { object_type; object_name; cascade = i == 1 })

let statement =
  ws *> peek_char_fail
  >>= (function 'C' -> create | 'D' -> drop | _ -> fail "Not supported")
  <* sc
  <?> "statement"

let statements = many statement <?> "statements"
