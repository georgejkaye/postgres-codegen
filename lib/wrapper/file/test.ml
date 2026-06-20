open Core

let ( / ) = Fpath.( / )
let ( // ) = Fpath.( // )

type mock_file_contents = String of string | Directory of mock_file list
and mock_file = { name : string; contents : mock_file_contents }

module Test_file_wrapper : Wrapper_t.File_wrapper_t = struct
  type state = mock_file

  let file_system_action root path ~f ~create =
    let rec file_system_action' parent root segs =
      match segs with
      | [] -> failwith "empty"
      | seg :: [] -> (
          match root.contents with
          | String _ when String.equal seg root.name ->
              let res, file = f parent root in
              (Some res, file)
          | Directory _ when String.equal seg "" ->
              let res, file = f parent root in
              (Some res, file)
          | _ -> (None, Some root))
      | seg :: next_seg :: remaining_segs -> (
          match root.contents with
          | String _ -> (None, Some root)
          | Directory files_in_directory ->
              if String.equal root.name seg then
                if String.equal next_seg "" then
                  let res, file = f parent root in
                  (Some res, file)
                else
                  let next_parent =
                    Some
                      (match parent with
                      | None -> Fpath.v seg
                      | Some parent -> parent / seg)
                  in
                  let res, updated_files =
                    List.fold_right files_in_directory ~init:(None, [])
                      ~f:(fun current_file (res, acc_files) ->
                        match res with
                        | Some _ -> (res, current_file :: acc_files)
                        | None ->
                            let res, updated_file =
                              file_system_action' next_parent current_file
                                (next_seg :: remaining_segs)
                            in
                            let updated_files =
                              match updated_file with
                              | None -> acc_files
                              | Some file -> file :: acc_files
                            in
                            (res, updated_files))
                  in
                  let res, updated_files =
                    match res with
                    | None when create ->
                        let new_file_contents =
                          match next_seg :: remaining_segs with
                          | "" :: [] -> Directory []
                          | _ :: [] -> String ""
                          | _ -> Directory []
                        in
                        let res, new_file =
                          file_system_action' next_parent
                            { name = next_seg; contents = new_file_contents }
                            (next_seg :: remaining_segs)
                        in
                        let updated_files =
                          match new_file with
                          | None -> updated_files
                          | Some file -> file :: updated_files
                        in
                        (res, updated_files)
                    | _ -> (res, updated_files)
                  in
                  ( res,
                    Some
                      { name = root.name; contents = Directory updated_files }
                  )
              else (None, Some root))
    in
    match file_system_action' None root (Fpath.segs path) with
    | res, Some p -> (res, p)
    | res, None -> (res, { name = root.name; contents = Directory [] })

  let init_state = { name = ""; contents = Directory [] }

  let get_file state p =
    match
      file_system_action state p ~create:false ~f:(fun parent f ->
          ((Util.Path.append_child parent f.name, f), Some f))
    with
    | Some f, _ -> Some f
    | None, _ -> None

  let file_exists state p =
    match get_file state p with Some _ -> `Yes | None -> `No

  let is_dir state p =
    match get_file state p with
    | Some (_, { name = _; contents = Directory _ }) -> `Yes
    | _ -> `No

  let read_file state p =
    match get_file state p with
    | Some (_, file) -> (
        match file.contents with
        | String s -> First s
        | Directory _ -> Second "file is a directory")
    | None -> Second "file does not exist"

  let write_file state p contents =
    let _, state =
      file_system_action state p ~create:true ~f:(fun _ f ->
          ((), Some { name = f.name; contents = String contents }))
    in
    state

  let files_of_directory state ?(filter = fun _ -> true) ?(recurse = false) p =
    let res, _ =
      file_system_action state p ~create:false ~f:(fun parent f ->
          let res =
            match f.contents with
            | String _ -> Second "file is not a directory"
            | Directory files ->
                let rec files_of_directory' parent files =
                  List.rev
                    (List.fold_right files ~init:[] ~f:(fun file acc ->
                         let full_path =
                           Util.Path.append_child parent file.name
                         in
                         if not (filter full_path) then acc
                         else
                           let acc = full_path :: acc in
                           if not recurse then full_path :: acc
                           else
                             match file.contents with
                             | String _ -> full_path :: acc
                             | Directory files ->
                                 files_of_directory' (Some full_path) files
                                 @ acc))
                in
                First (files_of_directory' parent files)
          in
          (res, Some f))
    in
    match res with Some res -> res | None -> Second "file does not exist"
end
