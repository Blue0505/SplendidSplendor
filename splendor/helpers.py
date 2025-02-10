import splendor.ansi_escape_codes as ansi

def gem_array_str(gem_array, gold=None) -> str:
  """Returns a string reprsentation of a gem array and gold."""
  output = (f"{ansi.WHITE}{gem_array[0]} {ansi.BLUE}{gem_array[1]} "
            f"{ansi.GREEN}{gem_array[2]} {ansi.RED}{gem_array[3]} "
            f"{ansi.GRAY}{gem_array[4]}{ansi.RESET}")

  if gold is not None:
    output += f" {ansi.YELLOW}{gold}{ansi.RESET}"
  return output