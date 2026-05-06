module type File_wrapper = sig
  val read_file : string -> string
  val write_file : string -> string -> unit
end
