program weighted_option_value_profile
implicit none
real :: initial(2), learning(2), flex(2), rev(2), scale(2), modu(2), lockin(2), cost(2), gov(2), ethics(2), score(2), warn(2)
integer :: i
initial=(/.58,.86/); learning=(/.82,.30/); flex=(/.78,.28/); rev=(/.74,.22/); scale=(/.70,.80/); modu=(/.64,.24/); lockin=(/.32,.82/); cost=(/.46,.34/); gov=(/.70,.48/); ethics=(/.68,.36/)
do i=1,2
 score(i)=.10*initial(i)+.17*learning(i)+.17*flex(i)+.12*rev(i)+.11*scale(i)+.13*modu(i)-.14*lockin(i)-.06*cost(i)+.11*gov(i)+.09*ethics(i)
 warn(i)=.30*lockin(i)+.18*(1-rev(i))+.16*(1-flex(i))+.14*(1-modu(i))+.12*(1-gov(i))+.10*(1-ethics(i))
 print *, i, score(i), warn(i)
end do
end program weighted_option_value_profile
