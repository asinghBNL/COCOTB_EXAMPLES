library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;

entity var_delay is
  generic(
    N : integer;
    D : integer
  );
  port (
    clk : in std_logic;
    rst : in std_logic;
    del : in std_logic_vector(N-1 downto 0);
    din : in std_logic_vector(N-1 downto 0);
    dout : out std_logic_vector(N-1 downto 0)
  );
end entity var_delay;

architecture rtl of var_delay is
  
  type delay_pipe is array(0 to D-1) of std_logic_vector(N-1 downto 0);
  signal pipe : delay_pipe := (others => (others => '0'));
  signal toggle : std_logic := '0'; --serves as a "divide by 2" for the clock, reduces size of delay pipeline
  signal vdel : integer := 0;

begin
  
  process(clk)
  begin
    if(rising_edge(clk)) then
      toggle <= not toggle;
    end if;
  end process;

  process(clk)
  begin
    if(rising_edge(clk)) then
      if (rst = '1') then
        pipe <= (others => (others => '0'));
      elsif(toggle = '1') then
        pipe <= din&pipe(0 to pipe'length-2);
      end if;
    end if;
  end process;
  
  vdel <= to_integer(unsigned(del));
  dout <= pipe(pipe'length - 1 - (vdel));
 

end architecture rtl;
