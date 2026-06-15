open Core

type triplet = Yes | Unknown | No

module type File_wrapper_t = sig
  type state

  val init_state : state
  val file_exists : state -> Fpath.t -> [ `Yes | `No | `Unknown ]
  val is_dir : state -> Fpath.t -> [ `Yes | `No | `Unknown ]
  val read_file : state -> Fpath.t -> (string, string) Either.t
  val write_file : state -> Fpath.t -> string -> state

  val files_of_directory :
    state ->
    ?filter:(Fpath.t -> bool) ->
    ?recurse:bool ->
    Fpath.t ->
    Fpath.t list
end
