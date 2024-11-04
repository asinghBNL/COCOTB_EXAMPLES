library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;

entity adder is
  generic(
    N : integer := 16
  );
  port (
    clk : in std_logic;
    a : in std_logic_vector(N-1 downto 0);
    b : in std_logic_vector(N-1 downto 0);
    c : out std_logic_vector(N-1 downto 0) := (others => '0')
  );
end entity adder;

architecture rtl of adder is
  
begin
  
  process(clk)
  begin
    if rising_edge(clk) then
      c <= std_logic_vector(signed(a) + signed(b));
    end if;
  end process;
  
end architecture rtl;
