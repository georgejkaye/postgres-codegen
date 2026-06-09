open Core

module type File_wrapper_t = sig
  val read_file : Fpath.t -> (string, string) Either.t
  val write_file : Fpath.t -> string -> unit
end
