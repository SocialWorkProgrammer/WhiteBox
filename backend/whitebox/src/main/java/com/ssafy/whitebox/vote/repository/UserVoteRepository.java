package com.ssafy.whitebox.vote.repository;

import com.ssafy.whitebox.vote.entity.UserVote;
import org.springframework.data.jpa.repository.JpaRepository;

import com.ssafy.whitebox.user.entity.User;
import com.ssafy.whitebox.vote.entity.Vote;


import java.util.Optional;

public interface UserVoteRepository extends JpaRepository<UserVote, Long> {
//    UserVote findByAiIndexAndVoterUserIndex(Long aiIndex, Long voterUserIndex);
    Optional<UserVote> findByUserAndVote(User user, Vote vote);
}
