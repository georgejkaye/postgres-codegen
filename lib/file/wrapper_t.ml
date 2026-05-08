open Core

module type File_wrapper_t = sig
  val read_file : string -> (string, string) Either.t
  val write_file : string -> string -> unit
end
