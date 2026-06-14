open Angstrom
open Postgres.Statement
open Postgres
open Util
open Combinators

let ws_or_comment =
  let rec go () =
    ws *> peek_char >>= function
    | Some '-' -> (
        char '-' *> peek_char >>= function
        | Some '-' -> (
            skip_while (function '\n' -> false | _ -> true) *> peek_char
            >>= function
            | None -> return ()
            | Some '\n' -> char '\n' *> go ()
            | _ -> fail "blah" *> go ())
        | _ -> return ())
    | _ -> return ()
  in
  go ()

let function_header_keywords = [ "LANGUAGE"; "RETURNS"; "AS" ]
let lb = char_p '(' ws_or_comment
let rb = char_p ')' ws_or_comment
let comma = char_p ',' ws_or_comment
let double_dollars = string_ci_p "$$" ws_or_comment <?> "expected $$"
let sc = char_p ';' ws_or_comment
let keyword kw = string_ci_p kw ws_or_comment <?> "expected keyword " ^ kw
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
let comment = string "--" *> take_till_char '\n' *> return ()
let or_replace = or_keyword *> replace_keyword

let variable_name =
  take_while1 (function
    | ' ' | ',' | '(' | ')' | ';' | '\n' | '\r' -> false
    | _ -> true)
  <* ws_or_comment
  <?> "variable_name"

let parameter_type =
  take_while1 (function ')' | ',' -> false | _ -> true) >>= fun t ->
  return (Postgres.Types.postgres_type_of_string (String.strip t))
  <* ws_or_comment
  <?> "type_name"

let param_and_type =
  variable_name ^^ parameter_type >>= fun (parameter_name, parameter_type) ->
  let open Parameter in
  return { parameter_name; parameter_type } <?> "param_and_type"

let bracketed_params =
  lb *> sep_by comma param_and_type
  <* ws_or_comment
  <* rb
  <?> "bracketed_params"

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
        return (Postgres.Types.postgres_type_of_string (String.strip t))
        <* ws_or_comment)
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
   Object.Function
     {
       function_name;
       function_parameters;
       function_return;
       function_language;
       function_body;
     })
  <?> "function_statement"

let type_statement =
  let+ composite_name = variable_name
  and+ _ = as_keyword
  and+ composite_fields = bracketed_params in
  Object.Composite { composite_name; composite_fields }

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
  Object.Domain { domain_name; underlying_type; domain_constraint }

let view_body = take_till_char ';'

let view_statement =
  let+ view_name = variable_name
  and+ _ = as_keyword
  and+ view_body = view_body in
  Object.View { view_name; view_body }

let object_type =
  peek_char_fail >>= function
  | 'F' -> function_keyword *> return Object_type.Function
  | 'T' -> type_keyword *> return Object_type.Composite
  | 'D' -> domain_keyword *> return Object_type.Domain
  | 'V' -> view_keyword *> return Object_type.View
  | _ -> fail "unsupported drop" <?> "drop"

let create =
  (let+ _ = create_keyword
   and+ or_replace_i, _ = at_most_one or_replace
   and+ object_data =
     object_type >>= fun a ->
     match a with
     | Object_type.Function -> function_statement
     | Object_type.Composite -> type_statement
     | Object_type.Domain -> domain_statement
     | Object_type.View -> view_statement
   in
   Create { object_data; or_replace = Int.equal or_replace_i 1 })
  <?> "create"

let if_exists = if_keyword *> exists_keyword

let drop =
  let+ _ = drop_keyword
  and+ object_type = object_type
  and+ if_exists_i, _ = at_most_one if_exists
  and+ object_name = variable_name
  and+ cascade_i, _ = at_most_one cascade_keyword in
  Drop
    {
      object_type;
      object_name;
      if_exists = Int.equal if_exists_i 1;
      cascade = Int.equal cascade_i 1;
    }

let statement =
  ws_or_comment *> peek_char
  >>= (function
        | Some 'C' -> create >>= fun s -> return (Some s)
        | Some 'D' -> drop >>= fun s -> return (Some s)
        | _ -> return None)
  <* sc
  <?> "statement"

let statements = many statement <?> "statements"
