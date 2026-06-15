open Core

type mock_file_contents =
  | String of string
  | Directory of mock_file list
  | Nonexistent

and mock_file = { name : string; contents : mock_file_contents }

module Test_file_wrapper : Wrapper_t.File_wrapper_t = struct
  type state = mock_file_contents

  let file_system_action state path ~create_dirs f =
    let rec file_system_action' state = function
      | [] -> f state
      | seg :: segs -> (
          match state with
          | String _ -> (None, state)
          | Directory files -> (
              if String.equal seg "" then f state
              else
                let res, updated_files =
                  List.fold_right
                    ~f:(fun cur (acc, state) ->
                      match acc with
                      | Some x -> (Some x, cur :: state)
                      | None ->
                          if String.equal cur.name seg then
                            let res, updated_file =
                              file_system_action' cur.contents segs
                            in
                            ( res,
                              { name = cur.name; contents = updated_file }
                              :: state )
                          else (None, cur :: state))
                    ~init:(None, []) files
                in
                match res with
                | None ->
                    if create_dirs then
                      let res, new_state =
                        file_system_action' (Directory []) segs
                      in
                      ( res,
                        Directory
                          ({ name = seg; contents = new_state } :: updated_files)
                      )
                    else (None, Directory updated_files)
                | Some res -> (Some res, Directory updated_files)))
    in
    file_system_action' state (Fpath.segs path)

  let get_file state path =
    let rec get_file' state = function
      | [] -> None
      | [ "" ] -> Some (Directory state)
      | [ x ] ->
          List.find
            ~f:(function File (name, _) -> String.equal name x | _ -> false)
            state
      | x :: xs ->
          List.find ~f:(function Directory (name, files) ->
              String.equal name x && file_exists' files xs)
      | _ -> false state
    in
    get_file' state (Fpath.segs path)

  let file_exists state p =
    get_file state f |> function Some _ -> `Yes | _ -> `No

  let is_dir state p =
    get_file state p |> function Some (Directory _) -> `Yes | _ -> `No

  let delete_path state path =
    List.filter
      ~f:(fun (candidate_path, _) -> not (Fpath.equal path candidate_path))
      state

  let init_state = Directory []

  let read_file (state : mock_file list) path =
    match file_exists state path with
    | Some (_, contents) -> First contents
    | None -> Second "Could not find file"

  let write_file (state : mock_file list) path contents =
    update_file state path contents

  let files_of_directory state ?(filter = fun _ -> true) ?(recurse = false)
      dir_path =
    failwith "todo"
end
