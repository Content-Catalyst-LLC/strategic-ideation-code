! Weighted prototype evidence profile example.
! Compile: gfortran weighted_prototype_evidence_profile.f90 -o weighted_prototype_evidence_profile
! Run: ./weighted_prototype_evidence_profile

program weighted_prototype_evidence_profile
  implicit none

  real :: assumption_clarity(3), learning_target_fit(3), evidence_quality(3), behavioral_grounding(3)
  real :: context_realism(3), systems_awareness(3), decision_linkage(3), ethical_review(3), learning_memory(3)
  real :: quality(3), theater(3)
  character(len=5) :: ids(3)
  integer :: i

  ids = (/"PE001", "PE004", "PE007"/)

  assumption_clarity = (/0.30, 0.84, 0.52/)
  learning_target_fit = (/0.28, 0.82, 0.46/)
  evidence_quality = (/0.26, 0.84, 0.40/)
  behavioral_grounding = (/0.22, 0.76, 0.26/)
  context_realism = (/0.34, 0.80, 0.32/)
  systems_awareness = (/0.24, 0.88, 0.30/)
  decision_linkage = (/0.20, 0.82, 0.38/)
  ethical_review = (/0.28, 0.72, 0.36/)
  learning_memory = (/0.22, 0.82, 0.34/)

  do i = 1, 3
     quality(i) = 0.13 * assumption_clarity(i) + &
                  0.13 * learning_target_fit(i) + &
                  0.15 * evidence_quality(i) + &
                  0.13 * behavioral_grounding(i) + &
                  0.11 * context_realism(i) + &
                  0.11 * systems_awareness(i) + &
                  0.11 * decision_linkage(i) + &
                  0.07 * ethical_review(i) + &
                  0.06 * learning_memory(i)

     theater(i) = 0.17 * (1.0 - assumption_clarity(i)) + &
                  0.16 * (1.0 - evidence_quality(i)) + &
                  0.14 * (1.0 - behavioral_grounding(i)) + &
                  0.13 * (1.0 - decision_linkage(i)) + &
                  0.12 * (1.0 - learning_memory(i)) + &
                  0.11 * (1.0 - systems_awareness(i)) + &
                  0.09 * (1.0 - ethical_review(i)) + &
                  0.08 * (1.0 - context_realism(i))
  end do

  print *, "Prototype learning quality and validation theater risk"
  do i = 1, 3
     print *, trim(ids(i)), quality(i), theater(i)
  end do
end program weighted_prototype_evidence_profile
