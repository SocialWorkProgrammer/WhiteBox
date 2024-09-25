package com.ssafy.whitebox.vote.repository;

import com.ssafy.whitebox.vote.entity.VoteComment;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import com.ssafy.whitebox.vote.entity.Vote;
import java.util.List;

@Repository
public interface VoteCommentRepository extends JpaRepository<VoteComment, Long> {
    List<VoteComment> findByVote(Vote vote);
}
