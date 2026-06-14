open Core

module type File_wrapper_t = sig
  type t_read
  type t_write

  val read_file : t_read -> Fpath.t -> (string, string) Either.t
  val write_file : t_write -> Fpath.t -> string -> t_write
end
