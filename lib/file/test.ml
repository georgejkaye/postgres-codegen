open Core

type mock_file = Fpath.t * string

module Test_file_wrapper : Wrapper_t.File_wrapper_t = struct
  type t_read = mock_file list
  type t_write = mock_file list

  let file_exists state path =
    List.find
      ~f:(fun (candidate_path, _) -> Fpath.equal path candidate_path)
      state

  let delete_path state path =
    List.filter
      ~f:(fun (candidate_path, _) -> not (Fpath.equal path candidate_path))
      state

  let read_file (state : mock_file list) path =
    match file_exists state path with
    | Some (_, contents) -> First contents
    | None -> Second "Could not find file"

  let write_file (state : mock_file list) path contents =
    (path, contents) :: delete_path state path
end
